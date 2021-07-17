package ru.aroize.queue.core

import io.reactivex.rxjava3.core.Single
import ru.aroize.network.cmd.user.GetUserCmd
import ru.aroize.network.dto.User
import ru.aroize.queue.utils.toSingle
import java.util.concurrent.ConcurrentHashMap

class UserRepository {

    private val memCache = ConcurrentHashMap<Int, User>()

    fun save(user: User) {
        memCache[user.id] = user
    }

    fun getUserById(id: Int): Single<User> {
        if (memCache.containsKey(id)) {
            return Single.just(memCache[id])
        }
        return GetUserCmd(id)
            .toSingle()
            .doOnSuccess { save(user = it) }
    }
}