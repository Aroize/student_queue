package ru.aroize.queue.dagger

import dagger.Component
import ru.aroize.queue.presentation.fragment.AuthFragment
import ru.aroize.queue.presentation.fragment.group.GroupsFragment
import ru.aroize.queue.presentation.fragment.RegisterFragment
import javax.inject.Singleton

@Singleton
@Component(modules = [RepositoryModule::class])
interface ApplicationComponent {
    fun inject(authFragment: AuthFragment)
    fun inject(registerFragment: RegisterFragment)
    fun inject(groupsFragment: GroupsFragment)
}