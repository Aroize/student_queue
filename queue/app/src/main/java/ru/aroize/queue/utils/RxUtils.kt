package ru.aroize.queue.utils

import io.reactivex.rxjava3.core.Single
import io.reactivex.rxjava3.schedulers.Schedulers
import ru.aroize.network.core.ApiCommand
import ru.aroize.network.core.ApiManager

fun<T> ApiCommand<T>.toSingle(): Single<T> {
    return Single.fromCallable { execute(ApiManager.default()) }
        .subscribeOn(Schedulers.io())
}