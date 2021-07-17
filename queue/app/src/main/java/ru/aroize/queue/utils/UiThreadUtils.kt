package ru.aroize.queue.utils

import android.os.Handler
import android.os.Looper

object UiThreadUtils {
    private val handler: Handler by lazy {
        Handler(Looper.getMainLooper())
    }

    fun post(runnable: Runnable) {
        handler.post(runnable)
    }

    fun post(runnable: Runnable, delay: Long) {
        handler.postDelayed(runnable, delay)
    }
}