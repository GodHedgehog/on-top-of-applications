package org.test.myapp;

import android.accessibilityservice.AccessibilityService;
import android.accessibilityservice.GestureDescription;
import android.content.Intent;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.IntentFilter;
import android.graphics.Path;
import android.view.accessibility.AccessibilityEvent;

public class MyAccessibilityService extends AccessibilityService {

    private BroadcastReceiver receiver;

    @Override
    protected void onServiceConnected() {
        // Регистрируем приёмник для Intent
        receiver = new BroadcastReceiver() {
            @Override
            public void onReceive(Context context, Intent intent) {
                if ("MY_ACCESSIBILITY_ACTION".equals(intent.getAction())) {
                    swipeUp();
                }
            }
        };
        IntentFilter filter = new IntentFilter("MY_ACCESSIBILITY_ACTION");
        registerReceiver(receiver, filter);
    }

    @Override
    public void onAccessibilityEvent(AccessibilityEvent event) {}

    @Override
    public void onInterrupt() {}

    private void swipeUp() {
        Path path = new Path();
        path.moveTo(500, 1500);
        path.lineTo(500, 500);

        GestureDescription.StrokeDescription stroke =
                new GestureDescription.StrokeDescription(path, 0, 300);

        GestureDescription.Builder builder = new GestureDescription.Builder();
        builder.addStroke(stroke);

        dispatchGesture(builder.build(), null, null);
    }
}
