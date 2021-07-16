package ru.aroize.network.core

interface ApiCommand<T> {
    fun execute(manager: ApiManager): T
}