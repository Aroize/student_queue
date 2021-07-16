package ru.aroize.network.utils

import org.json.JSONObject

class ApiException(
    val serverCode: Int,
    message: String
) : RuntimeException(message) {
    constructor(json: JSONObject) : this(
        json.getInt("code"),
        json.getString("message")
    )
}