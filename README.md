# firebase-unity-upm

Google's Firebase Unity SDK packages, mirrored so Unity Package Manager can install them by git URL.
Google publishes them only as tarballs at https://developers.google.com/unity/archive.

```json
"com.google.firebase.app": "https://github.com/fireplusteam/firebase-unity-upm.git?path=/com.google.firebase.app#14.0.0",
"com.google.firebase.analytics": "https://github.com/fireplusteam/firebase-unity-upm.git?path=/com.google.firebase.analytics#14.0.0"
```

Changes from Google's tarballs, made by `update.py`:

- The desktop (`x86_64`) and tvOS plugins are left out: Android and iOS only.
- `com.google.firebase.app` depends on Unity's `com.unity.external-dependency-manager` instead of Google's deprecated `com.google.external-dependency-manager`.

Each tag is an SDK version. Update: `python update.py <version>`, commit, tag `<version>`, push the tag.

The SDK is Apache 2.0, (c) Google LLC; each package keeps its `LICENSE.md`.
