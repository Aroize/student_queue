package ru.aroize.recycler

import android.content.Context
import android.util.AttributeSet
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.FrameLayout
import androidx.core.view.isVisible
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import androidx.swiperefreshlayout.widget.SwipeRefreshLayout
import ru.aroize.recycler.delegate.DelegateAdapter
import ru.aroize.recycler.delegate.ListItem
import ru.aroize.utils.PaginationList

class AdaptiveRecyclerView @JvmOverloads constructor(
    context: Context,
    attributeSet: AttributeSet? = null,
    defStyleAttr: Int = 0
): FrameLayout(context, attributeSet, defStyleAttr) {

    var loadingViewProvider: (Context, ViewGroup) -> View = { context, parent ->
        LayoutInflater.from(context).inflate(
            R.layout.default_loading_view, parent, false
        )
    }
    var errorViewProvider: (Context, ViewGroup) -> View = { context, parent ->
        LayoutInflater.from(context).inflate(
            R.layout.default_error_view, parent, false
        )
    }
    var emptyViewProvider: (Context, ViewGroup) -> View = { context, parent ->
        LayoutInflater.from(context).inflate(
            R.layout.default_empty_view, parent, false
        )
    }
    var layoutManagerProvider: (Context) -> RecyclerView.LayoutManager = {
        LinearLayoutManager(it, RecyclerView.VERTICAL, false)
    }

    lateinit var loadingView: View
    lateinit var errorView: View
    lateinit var emptyView: View
    lateinit var recyclerView: RecyclerView
    lateinit var swipeLayout: SwipeRefreshLayout

    fun bind(binder: PaginationBinder) {
        loadingView = loadingViewProvider.invoke(context, this)
        errorView = errorViewProvider.invoke(context, this)
        emptyView = emptyViewProvider.invoke(context, this)
        addView(loadingView, createDefaultLayoutParams())
        addView(errorView, createDefaultLayoutParams())

        val scrollListener = LoadMoreScrollListener(binder)

        recyclerView = RecyclerView(context)
        recyclerView.layoutManager = layoutManagerProvider.invoke(context)
        recyclerView.adapter = binder.adapter
        recyclerView.addOnScrollListener(scrollListener)

        swipeLayout = SwipeRefreshLayout(context)
        swipeLayout.setOnRefreshListener {
            val callback = PaginationBinder.OnItemsLoadedCallback {
                binder.adapter.setItems(it.list)
                scrollListener.hasMore = it.list.size < it.count
                swipeLayout.isRefreshing = false
            }
            binder.reload(callback)
        }
        val swipeContainer = FrameLayout(context)
        swipeContainer.addView(recyclerView, createDefaultLayoutParams())
        swipeContainer.addView(emptyView, createDefaultLayoutParams())
        swipeLayout.addView(swipeContainer, createDefaultLayoutParams())

        addView(swipeLayout, createDefaultLayoutParams())

        binder.loadMore(0) { list ->
            if (list.count == 0) {
                showEmpty()
            } else {
                showContent()
                binder.adapter.setItems(list.list)
                scrollListener.hasMore = list.list.size < list.count
            }
        }
    }

    fun showContent() {
        showFirstNHideOther(2, swipeLayout, recyclerView, loadingView, emptyView, errorView)
    }

    fun showEmpty() {
        showFirstNHideOther(2, emptyView, swipeLayout, recyclerView, loadingView, errorView)
    }

    fun showError() {
        showFirstNHideOther(1, errorView, loadingView, swipeLayout)
    }

    fun showLoading() {
        showFirstNHideOther(1, loadingView, swipeLayout, emptyView, errorView)
    }

    private fun showFirstNHideOther(n: Int, vararg views: View) {
        for (i in views.indices) {
            views[i].isVisible = i < n
        }
    }

    private fun createDefaultLayoutParams(): ViewGroup.LayoutParams {
        return ViewGroup.LayoutParams(
            ViewGroup.LayoutParams.MATCH_PARENT,
            ViewGroup.LayoutParams.MATCH_PARENT
        )
    }

    interface PaginationBinder {

        fun interface OnItemsLoadedCallback {
            fun onLoad(items: PaginationList<ListItem>)
        }

        val adapter: DelegateAdapter
        fun loadMore(offset: Int, callback: OnItemsLoadedCallback)
        fun reload(callback: OnItemsLoadedCallback)

        fun loadMoreBefore(): Int = 5
    }
}