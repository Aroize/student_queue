package ru.aroize.network.dto

import org.json.JSONObject

data class User(
    val id: Int,
    val login: String,
    val email: String,
    val name: String,
    val surname: String
) {
    companion object {
        fun parse(json: JSONObject) = User(
            json.optInt("id"),
            json.optString("login"),
            json.optString("email"),
            json.optString("name"),
            json.optString("surname")
        )
    }
}
