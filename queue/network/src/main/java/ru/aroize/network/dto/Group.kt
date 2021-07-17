package ru.aroize.network.dto

import org.json.JSONObject

data class Group(
    val id: Int,
    val admin: Int,
    val title: String,
    var size: Int = 0,
    var members: MutableList<User> = mutableListOf()
) {
    companion object {
        fun parse(json: JSONObject) = Group(
            id = json.getInt("id"),
            admin = json.getInt("admin"),
            title = json.getString("title"),
            size = json.optInt("size")
        )
    }
}
