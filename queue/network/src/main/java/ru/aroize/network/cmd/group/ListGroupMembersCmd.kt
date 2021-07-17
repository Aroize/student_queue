package ru.aroize.network.cmd.group

import org.json.JSONObject
import ru.aroize.network.core.BaseCommand
import ru.aroize.network.dto.User
import ru.aroize.utils.PaginationList
import ru.aroize.network.utils.map

class ListGroupMembersCmd(
    group: Int,
    offset: Int = -1,
    count: Int = -1
) : BaseCommand<ru.aroize.utils.PaginationList<User>>("group.members") {

    init {
        addParam("id", group)
        if (offset != - 1) addParam("offset", offset)
        if (count != -1) addParam("count", count)
    }

    override fun parse(json: JSONObject): ru.aroize.utils.PaginationList<User> {
        val count = json.getInt("count")
        val members = json.getJSONArray("members").map { User.parse(it) }
        return ru.aroize.utils.PaginationList(count, members)
    }
}