package ru.aroize.recycler.delegate

import android.view.View
import android.view.ViewGroup
import androidx.recyclerview.widget.RecyclerView

abstract class ViewTypeDelegate<T : ViewTypeDelegate.ViewTypeViewHolder> {

    abstract class ViewTypeViewHolder(item: View) : RecyclerView.ViewHolder(item) {
        abstract fun bind(item: ListItem)
    }

    abstract fun isForViewType(item: ListItem): Boolean
    abstract fun createViewHolder(parent: ViewGroup): T

    open fun bindViewHolder(holder: T, item: ListItem) {
        holder.bind(item)
    }
}