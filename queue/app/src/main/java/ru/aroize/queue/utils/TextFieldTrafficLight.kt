package ru.aroize.queue.utils

import android.text.Editable
import android.text.TextWatcher

class TextFieldTrafficLight(
    size: Int,
    private val redLight: () -> Unit,
    private val greenLight: () -> Unit
) {
    private val successMask = (1 shl size) - 1
    private var trafficLight = 0

    fun activate(position: Int) {
        val bit = 1 shl position
        trafficLight = trafficLight or bit
        callback()
    }

    fun deactivate(position: Int) {
        val bit = 1 shl position
        val negateMask = successMask xor bit
        trafficLight = trafficLight and negateMask
        callback()
    }

    private fun callback() {
        if (trafficLight == successMask) {
            greenLight.invoke()
        } else {
            redLight.invoke()
        }
    }

    class TextFieldWatcher(
        private val position: Int,
        private val trafficLight: TextFieldTrafficLight,
        private val textPredicate: (String) -> Boolean
    ) : TextWatcher {
        override fun afterTextChanged(s: Editable?) = Unit
        override fun beforeTextChanged(s: CharSequence?, start: Int, count: Int, after: Int) = Unit

        override fun onTextChanged(s: CharSequence?, start: Int, before: Int, count: Int) {
            s ?: return
            val text = s.toString()
            if (textPredicate.invoke(text)) {
                trafficLight.activate(position)
            } else {
                trafficLight.deactivate(position)
            }
        }
    }
}