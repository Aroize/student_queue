package ru.aroize.prefs

import android.content.Context

object PreferenceManager {

    private const val PREF_NAME = "main.prefs"

    private lateinit var appContext: Context

    fun init(appContext: Context) {
        PreferenceManager.appContext = appContext
    }

    fun set(key: String, value: Int) {
        appContext.getSharedPreferences(PREF_NAME, Context.MODE_PRIVATE)
            .edit()
            .putInt(key, value)
            .apply()
    }

    fun set(key: String, value: String) {
        appContext.getSharedPreferences(PREF_NAME, Context.MODE_PRIVATE)
            .edit()
            .putString(key, value)
            .apply()
    }

    fun int(key: String, default: Int = 0): Int {
        return appContext.getSharedPreferences(PREF_NAME, Context.MODE_PRIVATE)
            .getInt(key, default)
    }

    fun string(key: String): String? {
        return appContext.getSharedPreferences(PREF_NAME, Context.MODE_PRIVATE)
            .getString(key, null)
    }

    fun string(key: String, default: String): String {
        return string(key) ?: default
    }
}