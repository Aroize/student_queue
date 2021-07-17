package ru.aroize.queue.presentation.fragment.group

import android.view.LayoutInflater
import android.view.ViewGroup
import android.widget.ImageView
import android.widget.TextView
import androidx.appcompat.widget.AppCompatImageView
import androidx.core.view.isVisible
import ru.aroize.network.core.ApiManager
import ru.aroize.network.dto.Group
import ru.aroize.queue.R
import ru.aroize.queue.presentation.view.AbbreviationDrawable
import ru.aroize.recycler.delegate.ListItem
import ru.aroize.recycler.delegate.ViewTypeDelegate

class GroupItemDelegate : ViewTypeDelegate<GroupItemDelegate.GroupViewHolder>() {

    override fun isForViewType(item: ListItem): Boolean {
        return item is GroupListItem
    }

    override fun createViewHolder(parent: ViewGroup): GroupViewHolder {
        return GroupViewHolder(parent)
    }

    class GroupViewHolder(
        parent: ViewGroup
    ) : ViewTypeViewHolder(
        LayoutInflater.from(parent.context).inflate(R.layout.group_item, parent, false)
    ) {

        private val avatar: AppCompatImageView = itemView.findViewById(R.id.group_avatar)
        private val title: TextView = itemView.findViewById(R.id.group_title)
        private val size: TextView = itemView.findViewById(R.id.group_size)
        private val admin: ImageView = itemView.findViewById(R.id.admin_icon)

        override fun bind(item: ListItem) {
            item as GroupListItem

            title.text = item.group.title

            val sizeText = itemView.context.resources
                .getQuantityString(R.plurals.members, item.group.size, item.group.size)
            size.text = sizeText

            admin.isVisible = item.group.admin == ApiManager.default().userId

            var abbreviationDrawable = avatar.drawable as? AbbreviationDrawable
            if (abbreviationDrawable == null) {
                abbreviationDrawable = AbbreviationDrawable().apply { title = item.group.title }
                avatar.setImageDrawable(abbreviationDrawable)
            } else {
                abbreviationDrawable.title = item.group.title
            }
        }
    }

    class GroupListItem(val group: Group) : ListItem {
        override fun areItemsTheSame(other: ListItem): Boolean {
            return other is GroupListItem && other.group.id == group.id
        }

        override fun areContentsTheSame(other: ListItem): Boolean {
            other as GroupListItem
            return other.group.title == group.title && other.group.size == group.size
        }
    }
}