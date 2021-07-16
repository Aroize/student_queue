package ru.aroize.network.core

data class ApiConfig(
    val scheme: String,
    val host: String,
    val port: Int,
    val version: String
)