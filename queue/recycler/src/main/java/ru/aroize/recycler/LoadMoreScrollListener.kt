package ru.aroize.recycler

import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView

class LoadMoreScrollListener(
    private val binder: AdaptiveRecyclerView.PaginationBinder
): RecyclerView.OnScrollListener() {

    var hasMore: Boolean = true

    override fun onScrollStateChanged(recyclerView: RecyclerView, newState: Int) {
        if (newState == RecyclerView.SCROLL_STATE_IDLE && hasMore) {
            (recyclerView.layoutManager as? LinearLayoutManager)?.let { manager ->
                val last = manager.findLastVisibleItemPosition()
                if (last + binder.loadMoreBefore() >= binder.adapter.itemCount) {
                    val callback = AdaptiveRecyclerView.PaginationBinder.OnItemsLoadedCallback {
                        binder.adapter.setItems(it.list)
                        hasMore = it.list.size < it.count
                    }
                    binder.loadMore(binder.adapter.itemCount, callback)
                }
            }
        }
    }
}