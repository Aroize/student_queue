package ru.aroize.utils

data class PaginationList<T>(
    val count: Int,
    val list: List<T>
)