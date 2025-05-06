// Top-level build file where you can add configuration options common to all sub-projects/modules.

plugins {
    alias(libs.plugins.android.application) apply false
    id("com.android.library") version "8.0.2" apply false

}
// Project-level build.gradle.kts

buildscript {
    dependencies {
        // Add this line if it's not already there
        classpath("com.google.gms:google-services:4.4.0")
    }
}






