package ru.aroize.network.cmd.auth

import org.json.JSONObject
import ru.aroize.network.core.BaseCommand
import ru.aroize.network.dto.User
import ru.aroize.network.utils.Credentials

class AuthCmd(
    email: String,
    password: String
) : BaseCommand<Pair<Credentials, User>>("auth.auth") {

    init {
        addParam("email", email)
        addParam("password", password)
    }

    override fun parse(json: JSONObject): Pair<Credentials, User> {

        val user = User.parse(json.getJSONObject("user"))

        val credentialsJson = json.getJSONObject("credentials")

        val credentials = Credentials(
            user.id,
            credentialsJson.getString("access_token"),
            credentialsJson.getString("refresh_token")
        )

        return credentials to user
    }
}