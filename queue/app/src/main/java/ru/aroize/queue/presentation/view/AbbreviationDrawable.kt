package ru.aroize.queue.presentation.view

import android.graphics.*
import android.graphics.drawable.Drawable
import kotlin.math.abs

class AbbreviationDrawable : Drawable() {

    private val colors = intArrayOf(
        Color.CYAN,
        Color.MAGENTA,
        Color.rgb(240, 120, 60)
    )
    private val circlePaint = Paint().apply {
        style = Paint.Style.FILL_AND_STROKE
    }
    private val textPaint = Paint().apply {
        color = Color.WHITE
    }
    private val textBounds = Rect()

    private var abbreviation: String = "AA"

    var title: String = "AA"
    set(value) {
        field = value
        updateAbbreviation()
    }

    override fun draw(canvas: Canvas) {
        val rect = bounds

        circlePaint.color = pickColor()
        canvas.drawCircle(
            rect.exactCenterX(),
            rect.exactCenterY(),
            rect.width().toFloat() / 2,
            circlePaint
        )
        val textSize = rect.height() / 2f
        textPaint.textSize = textSize

        textPaint.getTextBounds(abbreviation, 0, abbreviation.length, textBounds)

        canvas.drawText(
            abbreviation,
            rect.exactCenterX() - textBounds.exactCenterX(),
            rect.exactCenterY() - textBounds.exactCenterY(),
            textPaint
        )
    }

    private fun updateAbbreviation() {
        val words = title.split(Regex("[\\s]+"))
        abbreviation = if (words.size == 1) {
            val word = words.first()
            word
                .filter { it.isLetter() }
                .take(2)
                .map { it.toUpperCase() }
                .joinToString(separator = "")
        } else {
            words
                .take(2)
                .map { str -> str.first { it.isLetter() } }
                .joinToString(separator = "")
        }
        invalidateSelf()
    }

    private fun pickColor(): Int {
        return when(abbreviation.first()) {
            in 'A'..'J' -> colors[0]
            in 'J'..'T' -> colors[1]
            else -> colors[2]
        }
    }

    override fun setAlpha(alpha: Int) = Unit
    override fun setColorFilter(colorFilter: ColorFilter?) = Unit
    override fun getOpacity(): Int = PixelFormat.OPAQUE

}