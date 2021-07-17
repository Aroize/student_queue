package ru.aroize.queue.presentation.fragment.group

import android.view.LayoutInflater
import android.view.ViewGroup
import ru.aroize.queue.R
import ru.aroize.recycler.delegate.ListItem
import ru.aroize.recycler.delegate.ViewTypeDelegate

class LoadingDelegate : ViewTypeDelegate<LoadingDelegate.LoadingViewHolder>() {

    override fun isForViewType(item: ListItem) = item is LoadingItem

    override fun createViewHolder(parent: ViewGroup): LoadingViewHolder {
        return LoadingViewHolder(parent)
    }

    class LoadingViewHolder(parent: ViewGroup) : ViewTypeDelegate.ViewTypeViewHolder(
        LayoutInflater.from(parent.context).inflate(
            R.layout.loading_item, parent, false
        )
    ) {
        override fun bind(item: ListItem) = Unit
    }

    class LoadingItem : ListItem {
        override fun areItemsTheSame(other: ListItem): Boolean {
            return other is LoadingItem
        }

        override fun areContentsTheSame(other: ListItem) = true
    }
}