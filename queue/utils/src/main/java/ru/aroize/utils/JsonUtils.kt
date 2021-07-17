package ru.aroize.network.utils

import org.json.JSONArray
import org.json.JSONObject

inline fun<T> JSONArray.map(crossinline func: (JSONObject) -> T): List<T> {
    val result = ArrayList<T>(length())
    for (i in 0 until length()) {
        result.add(func.invoke(getJSONObject(i)))
    }
    return result
}