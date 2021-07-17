package ru.aroize.queue.domain.group

import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import io.reactivex.rxjava3.android.schedulers.AndroidSchedulers
import io.reactivex.rxjava3.disposables.Disposable
import ru.aroize.network.cmd.group.ListUserGroupsCmd
import ru.aroize.network.dto.Group
import ru.aroize.utils.PaginationList
import ru.aroize.queue.utils.toSingle
import java.util.concurrent.TimeUnit
import javax.inject.Inject
import kotlin.math.max
import kotlin.math.min

class GroupListViewModel @Inject constructor() : ViewModel() {

    private var loadingDisposable: Disposable? = null
    private var reloadDisposable: Disposable? = null

    val loading: MutableLiveData<Boolean> by lazy { MutableLiveData(true) }
    val error: MutableLiveData<String> by lazy { MutableLiveData() }
    val groups: MutableLiveData<PaginationList<Group>> by lazy { MutableLiveData() }

    fun load(offset: Int = 0) {
        val cached = groups.value
        if (cached != null && cached.count == offset) {
            return
        }
        if (loadingDisposable == null || loadingDisposable?.isDisposed == true) {
            loading.value = true
            loadingDisposable = ListUserGroupsCmd(offset, COUNT)
                .toSingle()
                .observeOn(AndroidSchedulers.mainThread())
                .doOnEvent { _, _ -> loading.value = false }
                .subscribe({ list ->
                    merge(list)
                }, {
                    error.value = it.message
                })
        }
    }

    private fun merge(list: PaginationList<Group>) {
        val cached = groups.value
        val result = cached?.copy(
            list.count,
            cached.list + list.list
        ) ?: list
        groups.value = result
    }

    fun reload() {
        if (reloadDisposable == null || reloadDisposable?.isDisposed == true) {
            reloadDisposable = ListUserGroupsCmd(0, REFRESH_MAX_SIZE)
                .toSingle()
                .observeOn(AndroidSchedulers.mainThread())
                .subscribe({ list ->
                    groups.value = list
                }, {
                    error.value = it.message
                })
        }
    }

    companion object {
        const val COUNT = 12
        const val REFRESH_MAX_SIZE = 100
    }
}