package ru.aroize.recycler.delegate

interface ListItem {
    fun areItemsTheSame(other: ListItem): Boolean
    fun areContentsTheSame(other: ListItem): Boolean
}