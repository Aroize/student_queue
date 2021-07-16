package ru.aroize.network.cmd.auth

import org.json.JSONObject
import ru.aroize.network.core.ApiManager
import ru.aroize.network.core.BaseCommand
import ru.aroize.network.utils.Credentials

class RefreshCredentialsCmd : BaseCommand<Credentials>("auth.refresh_credentials") {
    override fun parse(json: JSONObject): Credentials {
        val accessToken = json.getString("access_token")
        val refreshToken = json.getString("refresh_token")
        return Credentials(
            ApiManager.default().userId,
            accessToken,
            refreshToken
        )
    }
}