package ru.aroize.network.cmd.group

import org.json.JSONObject
import ru.aroize.network.core.BaseCommand
import ru.aroize.network.dto.Group

class CreateGroupCmd(title: String) : BaseCommand<Group>("group.create") {

    init {
        addParam("title", title)
    }

    override fun parse(json: JSONObject): Group {
        return Group.parse(json)
    }
}