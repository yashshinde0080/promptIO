"use client";

import React from "react";
import { Settings, User, Key, Bell, Shield, Paintbrush } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Switch } from "@/components/ui/switch";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { useAuthStore } from "@/store/auth-store";

export default function SettingsPage() {
  const { user } = useAuthStore();

  return (
    <div className="p-6 space-y-6 max-w-screen-xl mx-auto">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-white flex items-center gap-2">
          <Settings className="h-6 w-6 text-gray-400" />
          Settings
        </h1>
        <p className="text-gray-400 mt-1 text-sm">
          Manage your account preferences and application settings.
        </p>
      </div>

      <Tabs defaultValue="profile" className="space-y-6">
        <TabsList className="bg-white/5 border border-white/10 p-1 w-full flex overflow-x-auto justify-start h-auto scrollbar-none">
          <TabsTrigger value="profile" className="gap-2 data-[state=active]:bg-white/10">
            <User className="h-4 w-4" /> Profile
          </TabsTrigger>
          <TabsTrigger value="api-keys" className="gap-2 data-[state=active]:bg-white/10">
            <Key className="h-4 w-4" /> API Keys
          </TabsTrigger>
          <TabsTrigger value="appearance" className="gap-2 data-[state=active]:bg-white/10">
            <Paintbrush className="h-4 w-4" /> Appearance
          </TabsTrigger>
          <TabsTrigger value="notifications" className="gap-2 data-[state=active]:bg-white/10">
            <Bell className="h-4 w-4" /> Notifications
          </TabsTrigger>
        </TabsList>

        {/* Profile Tab */}
        <TabsContent value="profile" className="space-y-6 mt-0">
          <Card>
            <CardHeader>
              <CardTitle>Personal Information</CardTitle>
              <CardDescription>Update your personal details and how others see you.</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2 max-w-md">
                <Label htmlFor="name">Full Name</Label>
                <Input id="name" defaultValue={user?.name || ""} />
              </div>
              <div className="space-y-2 max-w-md">
                <Label htmlFor="email">Email Address</Label>
                <Input id="email" type="email" defaultValue={user?.email || ""} disabled className="bg-white/5 opacity-70" />
                <p className="text-xs text-gray-500">Contact support to change your email address.</p>
              </div>
              <Button className="mt-4">Save Changes</Button>
            </CardContent>
          </Card>

          <Card className="border-red-500/20 bg-red-500/5">
            <CardHeader>
              <CardTitle className="text-red-400">Danger Zone</CardTitle>
              <CardDescription>Permanently delete your account and all associated data.</CardDescription>
            </CardHeader>
            <CardContent>
              <Button variant="destructive" className="bg-red-500 hover:bg-red-600 text-white">
                Delete Account
              </Button>
            </CardContent>
          </Card>
        </TabsContent>

        {/* API Keys Tab */}
        <TabsContent value="api-keys" className="space-y-6 mt-0">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between">
              <div>
                <CardTitle>API Keys</CardTitle>
                <CardDescription>Manage keys used to authenticate API requests.</CardDescription>
              </div>
              <Button>Create New Key</Button>
            </CardHeader>
            <CardContent>
              <div className="rounded-lg border border-white/10 bg-white/5 p-8 text-center">
                <Key className="h-8 w-8 text-gray-500 mx-auto mb-3" />
                <h3 className="text-lg font-medium text-white mb-1">No API keys found</h3>
                <p className="text-sm text-gray-400">Generate an API key to access PromptIO programmatically.</p>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Appearance Tab */}
        <TabsContent value="appearance" className="space-y-6 mt-0">
          <Card>
            <CardHeader>
              <CardTitle>Appearance</CardTitle>
              <CardDescription>Customize the look and feel of the platform.</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center justify-between p-4 rounded-lg border border-white/10 bg-white/5">
                <div className="space-y-1">
                  <p className="font-medium text-white">Theme</p>
                  <p className="text-sm text-gray-400">Select your preferred color theme.</p>
                </div>
                <div className="flex bg-black/40 p-1 rounded-lg border border-white/10">
                  <button className="px-3 py-1.5 text-sm rounded-md bg-white/10 text-white font-medium">Dark</button>
                  <button className="px-3 py-1.5 text-sm rounded-md text-gray-400 hover:text-white">Light</button>
                  <button className="px-3 py-1.5 text-sm rounded-md text-gray-400 hover:text-white">System</button>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Notifications Tab */}
        <TabsContent value="notifications" className="space-y-6 mt-0">
          <Card>
            <CardHeader>
              <CardTitle>Notification Preferences</CardTitle>
              <CardDescription>Choose what updates you want to receive.</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center justify-between p-4 rounded-lg border border-white/10">
                <div className="space-y-1">
                  <p className="font-medium text-white">Email Notifications</p>
                  <p className="text-sm text-gray-400">Receive daily summaries and critical alerts.</p>
                </div>
                <Switch defaultChecked />
              </div>
              <div className="flex items-center justify-between p-4 rounded-lg border border-white/10">
                <div className="space-y-1">
                  <p className="font-medium text-white">Product Updates</p>
                  <p className="text-sm text-gray-400">Get notified about new features and improvements.</p>
                </div>
                <Switch defaultChecked />
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}
