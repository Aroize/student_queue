package ru.aroize.queue.dagger

import dagger.Module
import dagger.Provides
import ru.aroize.queue.core.UserRepository
import javax.inject.Singleton

@Module
class RepositoryModule {

    @Provides
    @Singleton
    fun provideUserRepository(): UserRepository = UserRepository()
}