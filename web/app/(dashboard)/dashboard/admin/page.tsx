"use client";

import React from "react";
import { Shield, Users, Activity, Database, Server, AlertCircle } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

export default function AdminPage() {
  const systemHealth = [
    { name: "API Gateway", status: "Operational", uptime: "99.99%", latency: "45ms" },
    { name: "Database", status: "Operational", uptime: "99.95%", latency: "12ms" },
    { name: "Model Router", status: "Degraded", uptime: "98.50%", latency: "850ms" },
    { name: "Cache Redis", status: "Operational", uptime: "100%", latency: "2ms" },
  ];

  return (
    <div className="p-6 space-y-6 max-w-screen-2xl mx-auto">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-white flex items-center gap-2">
          <Shield className="h-6 w-6 text-red-400" />
          Admin Panel
        </h1>
        <p className="text-gray-400 mt-1 text-sm">
          System health, global configuration, and user management.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card className="bg-gradient-to-br from-blue-500/10 to-transparent border-blue-500/20">
          <CardContent className="p-4 flex items-center gap-4">
            <div className="p-3 bg-blue-500/20 rounded-lg">
              <Users className="h-6 w-6 text-blue-400" />
            </div>
            <div>
              <p className="text-2xl font-bold text-white">1,248</p>
              <p className="text-sm text-gray-400">Total Users</p>
            </div>
          </CardContent>
        </Card>
        
        <Card className="bg-gradient-to-br from-emerald-500/10 to-transparent border-emerald-500/20">
          <CardContent className="p-4 flex items-center gap-4">
            <div className="p-3 bg-emerald-500/20 rounded-lg">
              <Activity className="h-6 w-6 text-emerald-400" />
            </div>
            <div>
              <p className="text-2xl font-bold text-white">84.2k</p>
              <p className="text-sm text-gray-400">API Calls (24h)</p>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-gradient-to-br from-violet-500/10 to-transparent border-violet-500/20">
          <CardContent className="p-4 flex items-center gap-4">
            <div className="p-3 bg-violet-500/20 rounded-lg">
              <Database className="h-6 w-6 text-violet-400" />
            </div>
            <div>
              <p className="text-2xl font-bold text-white">4.2 TB</p>
              <p className="text-sm text-gray-400">Storage Used</p>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-gradient-to-br from-red-500/10 to-transparent border-red-500/20">
          <CardContent className="p-4 flex items-center gap-4">
            <div className="p-3 bg-red-500/20 rounded-lg">
              <Server className="h-6 w-6 text-red-400" />
            </div>
            <div>
              <p className="text-2xl font-bold text-white flex items-center gap-2">
                1 <AlertCircle className="h-4 w-4 text-red-400" />
              </p>
              <p className="text-sm text-gray-400">Active Alerts</p>
            </div>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>System Health</CardTitle>
            <CardDescription>Real-time status of PromptIO services</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {systemHealth.map((service) => (
                <div key={service.name} className="flex items-center justify-between p-3 rounded-lg border border-white/5 bg-white/5">
                  <div className="flex items-center gap-3">
                    <div className={`h-2.5 w-2.5 rounded-full ${service.status === 'Operational' ? 'bg-emerald-400' : 'bg-red-400 animate-pulse'}`} />
                    <span className="font-medium text-sm text-white">{service.name}</span>
                  </div>
                  <div className="flex items-center gap-6 text-sm text-gray-400">
                    <div className="w-16 text-right">{service.latency}</div>
                    <div className="w-16 text-right">{service.uptime}</div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Recent Admin Actions</CardTitle>
            <CardDescription>Audit log of administrative changes</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {[
                { action: "Updated model routing rules", user: "system_admin", time: "10m ago" },
                { action: "Suspended account: test@spam.com", user: "moderator_1", time: "1h ago" },
                { action: "Increased rate limits for enterprise-org", user: "system_admin", time: "3h ago" },
                { action: "Deployed new evaluation models", user: "system", time: "1d ago" },
              ].map((log, i) => (
                <div key={i} className="flex items-start gap-3 text-sm">
                  <div className="h-2 w-2 rounded-full bg-blue-500 mt-1.5" />
                  <div>
                    <p className="text-white">{log.action}</p>
                    <p className="text-xs text-gray-500">by {log.user} • {log.time}</p>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
