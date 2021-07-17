package ru.aroize.queue.presentation.fragment.group

import android.content.Context
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.LinearLayout
import androidx.fragment.app.Fragment
import androidx.lifecycle.Observer
import androidx.recyclerview.widget.DividerItemDecoration
import androidx.recyclerview.widget.RecyclerView
import com.google.android.material.appbar.MaterialToolbar
import com.google.android.material.dialog.MaterialAlertDialogBuilder
import com.google.android.material.textfield.TextInputEditText
import com.google.android.material.textfield.TextInputLayout
import ru.aroize.network.dto.Group
import ru.aroize.queue.App
import ru.aroize.queue.R
import ru.aroize.queue.domain.group.GroupListViewModel
import ru.aroize.recycler.AdaptiveRecyclerView
import ru.aroize.recycler.delegate.DelegateAdapter
import ru.aroize.recycler.delegate.ListItem
import ru.aroize.utils.PaginationList
import javax.inject.Inject

class GroupsFragment : Fragment(), AdaptiveRecyclerView.PaginationBinder {

    @Inject lateinit var model: GroupListViewModel

    private lateinit var list: AdaptiveRecyclerView
    private lateinit var toolbar: MaterialToolbar

    private var callback: AdaptiveRecyclerView.PaginationBinder.OnItemsLoadedCallback? = null
    override val adapter: DelegateAdapter = GroupDelegateAdapter()
    override fun loadMore(
        offset: Int,
        callback: AdaptiveRecyclerView.PaginationBinder.OnItemsLoadedCallback
    ) {
        this.callback = callback
        val hasLoadingItem = adapter.items.isNotEmpty() && adapter.items.last() is LoadingDelegate.LoadingItem
        val loading = if (hasLoadingItem) 1  else 0
        model.load(offset - loading)
    }

    override fun reload(callback: AdaptiveRecyclerView.PaginationBinder.OnItemsLoadedCallback) {
        this.callback = callback
        model.reload()
    }

    override fun onAttach(context: Context) {
        super.onAttach(context)
        App.appComponent.inject(this)
    }

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        val root = inflater.inflate(R.layout.group_list_layout, container, false)
        list = root.findViewById(R.id.group_list)
        toolbar = root.findViewById(R.id.groups_toolbar)
        return root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {

        toolbar.setOnMenuItemClickListener {
            when (it.itemId) {
                R.id.create_group -> {
                    val editText = TextInputEditText(requireContext()).apply {
                        maxLines = 1
                    }
                    val dialog = TextInputLayout(requireContext()).apply {
                        addView(editText, LinearLayout.LayoutParams(
                            LinearLayout.LayoutParams.MATCH_PARENT,
                            LinearLayout.LayoutParams.WRAP_CONTENT
                        ))
                        hint = getString(R.string.group_title)
                    }

                    MaterialAlertDialogBuilder(requireContext())
                        .setView(dialog)
                        .show()
                    true
                }
                else -> false
            }
        }

        list.bind(this)
        list.recyclerView.addItemDecoration(DividerItemDecoration(
            list.recyclerView.context, RecyclerView.VERTICAL
        ))

        val loading = Observer<Boolean> { load ->
            if (!load) {
                list.showContent()
            } else {
                if (adapter.itemCount == 0) {
                    list.showLoading()
                }
            }
        }

        val groups = Observer<PaginationList<Group>> {
            val list: PaginationList<ListItem> = PaginationList(
                it.count,
                it.list.map { group -> GroupItemDelegate.GroupListItem(group) }
            )
            callback?.onLoad(list)
            if (it.count > it.list.size) {
                adapter.setItems(adapter.items + listOf(LoadingDelegate.LoadingItem()))
            }
        }

        model.loading.observe(viewLifecycleOwner, loading)
        model.groups.observe(viewLifecycleOwner, groups)

        model.load()
    }
}