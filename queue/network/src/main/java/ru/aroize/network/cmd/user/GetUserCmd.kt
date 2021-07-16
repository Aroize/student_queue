package ru.aroize.network.cmd.user

import org.json.JSONObject
import ru.aroize.network.core.BaseCommand
import ru.aroize.network.dto.User

class GetUserCmd(id: Int) : BaseCommand<User>("user.get") {

    init {
        addParam("id", id)
    }

    override fun parse(json: JSONObject): User {
        return User.parse(json)
    }
}