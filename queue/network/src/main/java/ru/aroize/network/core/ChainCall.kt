package ru.aroize.network.core

abstract class ChainCall<F, S, T>(
    private val first: ApiCommand<F>,
    private val second: ApiCommand<S>
) : ApiCommand<T> {

    abstract fun compose(first: F, second: S): T

    override fun execute(manager: ApiManager): T {
        val firstResponse = first.execute(manager)
        val secondResponse = second.execute(manager)
        return compose(firstResponse, secondResponse)
    }
}