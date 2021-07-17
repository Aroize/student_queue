package ru.aroize.recycler.delegate

import android.view.ViewGroup
import androidx.recyclerview.widget.DiffUtil
import androidx.recyclerview.widget.RecyclerView

open class DelegateAdapter : RecyclerView.Adapter<RecyclerView.ViewHolder>() {

    private val delegates: MutableList<ViewTypeDelegate<*>> = mutableListOf()
    var items: List<ListItem> = mutableListOf()
        private set

    override fun getItemCount(): Int = items.size

    override fun getItemViewType(position: Int): Int {
        val item = items[position]
        return findDelegateViewType(item)
    }

    @Suppress("UNCHECKED_CAST")
    override fun onBindViewHolder(holder: RecyclerView.ViewHolder, position: Int) {
        val item = items[position]
        val viewType = findDelegateViewType(item)
        val delegate = delegates[viewType] as ViewTypeDelegate<ViewTypeDelegate.ViewTypeViewHolder>
        delegate.bindViewHolder(holder as ViewTypeDelegate.ViewTypeViewHolder, item)
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): RecyclerView.ViewHolder {
        val delegate = delegates[viewType]
        return delegate.createViewHolder(parent)
    }

    fun setItems(newItems: List<ListItem>) {
        val callback = ListItemCallback(items, newItems)
        val result = DiffUtil.calculateDiff(callback)
        items = newItems
        result.dispatchUpdatesTo(this)
    }

    protected fun addDelegate(delegate: ViewTypeDelegate<*>) {
        delegates.add(delegate)
    }

    private fun findDelegateViewType(item: ListItem): Int {
        delegates.forEachIndexed { index, delegate ->
            if (delegate.isForViewType(item))
                return index
        }
        throw IllegalArgumentException("No delegate for this item")
    }
}