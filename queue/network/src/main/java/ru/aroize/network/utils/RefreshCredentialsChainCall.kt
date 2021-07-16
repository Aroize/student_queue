package ru.aroize.network.utils

import ru.aroize.network.cmd.auth.RefreshCredentialsCmd
import ru.aroize.network.core.ApiCommand
import ru.aroize.network.core.ApiManager
import ru.aroize.network.core.ChainCall

class RefreshCredentialsChainCall<T>(cmd: ApiCommand<T>) : ChainCall<Credentials, T, T>(
    RefreshCredentialsCmd(),
    cmd
) {
    override fun compose(first: Credentials, second: T): T {
        ApiManager.default().updateCredentials(first)
        return second
    }
}