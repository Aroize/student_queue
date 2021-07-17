package ru.aroize.recycler.delegate

import androidx.recyclerview.widget.DiffUtil

class ListItemCallback(
    private val old: List<ListItem>,
    private val new: List<ListItem>
) : DiffUtil.Callback() {

    override fun getNewListSize(): Int = new.size

    override fun getOldListSize(): Int = old.size

    override fun areItemsTheSame(oldItemPosition: Int, newItemPosition: Int): Boolean {
        return old[oldItemPosition].areItemsTheSame(new[newItemPosition])
    }

    override fun areContentsTheSame(oldItemPosition: Int, newItemPosition: Int): Boolean {
        return old[oldItemPosition].areContentsTheSame(new[newItemPosition])
    }
}