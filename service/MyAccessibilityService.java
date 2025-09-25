package org.test.myapp;

import android.accessibilityservice.AccessibilityService;
import android.accessibilityservice.GestureDescription;
import android.graphics.Path;
import android.view.accessibility.AccessibilityEvent;

public class MyAccessibilityService extends AccessibilityService {

    @Override
    public void onAccessibilityEvent(AccessibilityEvent event) {
        // Можно отлавливать события (необязательно)
    }

    @Override
    public void onInterrupt() {
    }

    // Метод для свайпа вверх
    public void swipeUp() {
        Path path = new Path();
        path.moveTo(500, 1500); // стартовые координаты
        path.lineTo(500, 500);  // конечные координаты

        GestureDescription.StrokeDescription stroke =
                new GestureDescription.StrokeDescription(path, 0, 300);

        GestureDescription.Builder builder = new GestureDescription.Builder();
        builder.addStroke(stroke);

        dispatchGesture(builder.build(), null, null);
    }
}
