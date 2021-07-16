package ru.aroize.network.utils

interface ApiCallback<T> {
    fun onSuccess(response: T)
    fun onError(e: Throwable)
}