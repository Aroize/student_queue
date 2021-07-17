package ru.aroize.queue.presentation.fragment.group

import ru.aroize.recycler.delegate.DelegateAdapter

class GroupDelegateAdapter : DelegateAdapter() {

    init {
        addDelegate(GroupItemDelegate())
        addDelegate(LoadingDelegate())
    }
}