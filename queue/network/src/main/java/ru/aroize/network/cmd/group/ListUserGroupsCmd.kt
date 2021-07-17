package ru.aroize.network.cmd.group

import org.json.JSONObject
import ru.aroize.network.core.BaseCommand
import ru.aroize.network.dto.Group
import ru.aroize.utils.PaginationList
import ru.aroize.network.utils.map

class ListUserGroupsCmd(
    offset: Int = -1,
    count: Int = -1
) : BaseCommand<ru.aroize.utils.PaginationList<Group>>("group.list") {

    init {
        if (offset != - 1) addParam("offset", offset)
        if (count != -1) addParam("count", count)
    }

    override fun parse(json: JSONObject): ru.aroize.utils.PaginationList<Group> {
        val count = json.getInt("count")
        val groups = json.getJSONArray("groups").map { Group.parse(it) }
        return ru.aroize.utils.PaginationList(count, groups)
    }
}