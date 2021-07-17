package ru.aroize.queue.presentation.fragment

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import androidx.fragment.app.viewModels
import androidx.lifecycle.Observer
import ru.aroize.queue.MainActivity
import ru.aroize.queue.R
import ru.aroize.queue.domain.splash.SplashViewModel

class SplashFragment : Fragment() {
    private val model: SplashViewModel by viewModels()

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        return inflater.inflate(R.layout.splash_layout, container, false)
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        val observer = Observer<Int> {
            when {
                it <= 0 -> (activity as MainActivity).openAuthPage()
                else -> (activity as MainActivity).openProfilePage(it)
            }
        }

        model.user.observe(viewLifecycleOwner, observer)
        model.attach()
    }
}