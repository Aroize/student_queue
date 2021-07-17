package ru.aroize.network.core

import org.json.JSONException
import org.json.JSONObject
import ru.aroize.network.utils.ApiException

abstract class BaseCommand<T>(
    private val method: String,
    private val id: Int = 0
) : ApiCommand<T> {

    private val params = JSONObject()

    protected fun addParam(key: String, value: Int) = params.put(key, value)
    protected fun addParam(key: String, value: String) = params.put(key, value)
    protected fun addParam(key: String, value: Boolean) = params.put(key, value)

    abstract fun parse(json: JSONObject): T

    override fun execute(manager: ApiManager): T {
        val body = JSONObject().apply {
            put("jsonrpc", ApiManager.JRPC_VERSION)
            put("method", method)
            put("id", id)
            put("params", params)
        }

        val client = manager.client()
        val request = manager.request(body.toString())

        val response = client.newCall(request).execute()

        if (!response.isSuccessful) {
            throw ApiException(-2, response.body!!.string())
        }

        val jsonString = response.body!!.string()
        return parse(jsonString)
    }

    @Throws(JSONException::class)
    fun parse(jsonString: String): T {
        val json = JSONObject(jsonString)

        val jrpc = json.getString("jsonrpc")

        if (jrpc != ApiManager.JRPC_VERSION)
            throw ApiException(-1, "JRPC specification version doesn't match")

        if (json.has("error"))
            throw ApiException(json.getJSONObject("error"))

        val response = json.getJSONObject("result")

        return parse(response)
    }
}