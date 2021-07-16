package ru.aroize.network.core

import android.os.Handler
import android.os.Looper
import okhttp3.*
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.RequestBody.Companion.toRequestBody
import ru.aroize.network.utils.*
import ru.aroize.network.utils.Credentials
import ru.aroize.prefs.PreferenceManager
import java.util.concurrent.Executors

class ApiManager {

    private val networkExecutor = Executors.newFixedThreadPool(32)
    private val mainHandler = Handler(Looper.getMainLooper())

    @Volatile
    private var credentials: Credentials? = null
    private lateinit var client: OkHttpClient
    private lateinit var config: ApiConfig

    var userId: Int = 0
    private set

    fun init(config: ApiConfig) {
        this.client = OkHttpClient()
        this.config = config
    }

    @Synchronized
    fun updateCredentials(credentials: Credentials) {
        this.userId = credentials.id
        this.credentials = credentials

        PreferenceManager.set("USER_ID", credentials.id)
        PreferenceManager.set("ACCESS_TOKEN", credentials.access)
        PreferenceManager.set("REFRESH_TOKEN", credentials.refresh)
    }

    fun<T> execute(cmd: ApiCommand<T>, callback: ApiCallback<T>) {
        networkExecutor.execute {
            try {
                val response = execute(cmd)
                mainHandler.post { callback.onSuccess(response) }
            } catch (t: Throwable) {
                mainHandler.post { callback.onError(t) }
            }
        }
    }

    fun<T> execute(cmd: ApiCommand<T>): T {
        try {
            return cmd.execute(this)
        } catch (e: RuntimeException) {
            if (e is ApiException && e.serverCode == 2) {
                val chain = wrapWithRefreshCmd(cmd)
                return execute(chain)
            }
            throw e
        }
    }

    internal fun client() = client
    internal fun request(json: String): Request {
        val url = HttpUrl.Builder()
            .scheme(config.scheme)
            .host(config.host)
            .port(config.port)
            .addPathSegment(config.version)
            .build()
        val builder = Request.Builder().url(url)
        credentials?.let {
            builder
                .header(ServerKeys.USER_ID_HEADER, it.id.toString())
                .header(ServerKeys.USER_ACCESS_HEADER, it.access)
                .header(ServerKeys.USER_REFRESH_HEADER, it.refresh)
        }
        val body = json.toRequestBody("application/json".toMediaType())
        return builder.post(body).build()
    }

    private fun<T> wrapWithRefreshCmd(cmd: ApiCommand<T>): ApiCommand<T> {
        return RefreshCredentialsChainCall(cmd)
    }

    companion object {

        const val JRPC_VERSION = "2.0"

        @Volatile
        private var default: ApiManager? = null

        @JvmStatic
        @Synchronized
        fun default(): ApiManager {
            if (default == null) {
                default = ApiManager()
            }
            return default!!
        }
    }
}