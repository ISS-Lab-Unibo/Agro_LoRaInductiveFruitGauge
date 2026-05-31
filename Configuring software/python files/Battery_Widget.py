# da https://github.com/god233012yamil/Battery-Widget-Using-Python

# Versione convertita per PyQt6

from math import floor
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QPen, QColor
from PyQt6.QtCore import Qt, QRect, QSize


class BatteryWidget(QWidget):

    def __init__(
        self,
        parent: QWidget = None,
        min_voltage: float = 0.0,
        max_voltage: float = 100.0,
        segments: int = 10,
        orientation: Qt.Orientation = Qt.Orientation.Horizontal,
    ) -> None:

        super().__init__(parent)
        self._voltage = 0.0
        self._min_voltage = min_voltage
        self._max_voltage = max_voltage
        self._segments = segments
        self._orientation = orientation

    @property
    def voltage(self) -> float:
        return self._voltage

    @voltage.setter
    def voltage(self, value: float) -> None:
        self._voltage = max(self._min_voltage, min(value, self._max_voltage))
        self.update()

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        pen_width = 2
        painter.setPen(QPen(Qt.GlobalColor.black, pen_width))

        rect = self.rect()

        if self._orientation == Qt.Orientation.Horizontal:
            self._draw_horizontal(painter, rect, pen_width)
        else:
            self._draw_vertical(painter, rect, pen_width)

    def _draw_horizontal(self, painter, rect, pen_width):
        battery_tip_width = rect.width() * 0.05
        battery_body_width = rect.width() - battery_tip_width - pen_width
        battery_height = rect.height() - pen_width

        body_rect = QRect(
            pen_width // 2,
            pen_width // 2,
            int(battery_body_width),
            int(battery_height),
        )
        painter.drawRect(body_rect)

        tip_rect = QRect(
            body_rect.right() + 1,
            int(rect.height() * 0.2),
            int(battery_tip_width),
            int(rect.height() * 0.6),
        )
        painter.drawRect(tip_rect)

        fill_ratio = (
            (self._voltage - self._min_voltage)
            / (self._max_voltage - self._min_voltage)
            if self._max_voltage > self._min_voltage
            else 0.0
        )
        fill_ratio = max(0.0, min(fill_ratio, 1.0))
        filled_segments = floor(fill_ratio * self._segments)

        padding = 4
        spacing = 4

        available_width = body_rect.width() - 2 * padding
        available_height = body_rect.height() - 2 * padding
        total_spacing = (self._segments - 1) * spacing

        segment_width = (
            (available_width - total_spacing) / self._segments
            if self._segments > 0
            else available_width
        )

        for i in range(self._segments):
            x = body_rect.left() + padding + i * (segment_width + spacing)
            y = body_rect.top() + padding

            segment_rect = QRect(
                int(x),
                int(y),
                int(segment_width),
                int(available_height),
            )

            if i < filled_segments:
                painter.fillRect(segment_rect, QColor(0, 200, 0))
            else:
                painter.fillRect(segment_rect, QColor(220, 220, 220))

            painter.drawRect(segment_rect)

    def _draw_vertical(self, painter, rect, pen_width):
        battery_tip_height = rect.height() * 0.05
        battery_body_height = rect.height() - battery_tip_height - pen_width
        battery_width = rect.width() - pen_width

        tip_rect = QRect(
            int(rect.width() * 0.2),
            pen_width // 2,
            int(rect.width() * 0.6),
            int(battery_tip_height),
        )
        painter.drawRect(tip_rect)

        body_rect = QRect(
            pen_width // 2,
            pen_width // 2 + int(battery_tip_height),
            int(battery_width),
            int(battery_body_height),
        )
        painter.drawRect(body_rect)

        fill_ratio = (
            (self._voltage - self._min_voltage)
            / (self._max_voltage - self._min_voltage)
            if self._max_voltage > self._min_voltage
            else 0.0
        )
        fill_ratio = max(0.0, min(fill_ratio, 1.0))
        filled_segments = floor(fill_ratio * self._segments)

        padding = 4
        spacing = 4
        available_width = body_rect.width() - 2 * padding
        available_height = body_rect.height() - 2 * padding
        total_spacing = (self._segments - 1) * spacing

        segment_height = (
            (available_height - total_spacing) / self._segments
            if self._segments > 0
            else available_height
        )

        for i in range(self._segments):
            x = body_rect.left() + padding
            y = body_rect.bottom() - padding - (i + 1) * (segment_height + spacing) + spacing

            segment_rect = QRect(
                int(x),
                int(y),
                int(available_width),
                int(segment_height),
            )

            if i < filled_segments:
                painter.fillRect(segment_rect, QColor(0, 200, 0))
            else:
                painter.fillRect(segment_rect, QColor(220, 220, 220))

            painter.drawRect(segment_rect)

    def sizeHint(self) -> QSize:
        return QSize(200, 100)