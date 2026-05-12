"use client";

import React, { useState } from "react";
import { Users, Mail, Plus, Search, Shield, MoreHorizontal, Trash2 } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Avatar } from "@/components/ui/avatar";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

const MOCK_TEAM = [
  { id: "1", name: "Alex Chen", email: "alex@company.com", role: "Owner", status: "Active" },
  { id: "2", name: "Sarah Kim", email: "sarah@company.com", role: "Admin", status: "Active" },
  { id: "3", name: "Marcus Liu", email: "marcus@company.com", role: "Editor", status: "Invited" },
  { id: "4", name: "Priya Patel", email: "priya@company.com", role: "Viewer", status: "Active" },
];

export default function TeamsPage() {
  const [search, setSearch] = useState("");

  const filteredTeam = MOCK_TEAM.filter(member => 
    member.name.toLowerCase().includes(search.toLowerCase()) || 
    member.email.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="p-6 space-y-6 max-w-screen-2xl mx-auto">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center gap-2">
            <Users className="h-6 w-6 text-emerald-400" />
            Team Settings
          </h1>
          <p className="text-gray-400 mt-1 text-sm">
            Manage your team members, roles, and access controls.
          </p>
        </div>
        <Button className="gap-2">
          <Plus className="h-4 w-4" />
          Invite Member
        </Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Main Content */}
        <div className="md:col-span-2 space-y-6">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between pb-4">
              <div>
                <CardTitle>Members</CardTitle>
                <CardDescription>People with access to this workspace</CardDescription>
              </div>
              <div className="w-64 relative">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                <Input
                  placeholder="Search members..."
                  value={search}
                  onChange={(e) => setSearch(e.target.value)}
                  className="pl-9"
                />
              </div>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {filteredTeam.map((member) => (
                  <div key={member.id} className="flex items-center justify-between p-3 rounded-lg hover:bg-white/5 transition-colors border border-transparent hover:border-white/10">
                    <div className="flex items-center gap-3">
                      <Avatar fallback={member.name} size="md" />
                      <div>
                        <div className="flex items-center gap-2">
                          <p className="font-medium text-white text-sm">{member.name}</p>
                          {member.status === "Invited" && (
                            <Badge variant="outline" className="text-[10px] py-0 h-4 border-yellow-500/30 text-yellow-400">Invited</Badge>
                          )}
                        </div>
                        <p className="text-xs text-gray-500">{member.email}</p>
                      </div>
                    </div>
                    
                    <div className="flex items-center gap-4">
                      <div className="flex items-center gap-1 text-xs text-gray-400 bg-white/5 px-2 py-1 rounded">
                        <Shield className="h-3 w-3" />
                        {member.role}
                      </div>
                      <DropdownMenu>
                        <DropdownMenuTrigger asChild>
                          <Button variant="ghost" size="icon" className="h-8 w-8 text-gray-400">
                            <MoreHorizontal className="h-4 w-4" />
                          </Button>
                        </DropdownMenuTrigger>
                        <DropdownMenuContent align="end" className="w-40 border-border/50">
                          <DropdownMenuItem>Change Role</DropdownMenuItem>
                          {member.status === "Invited" && <DropdownMenuItem>Resend Invite</DropdownMenuItem>}
                          <DropdownMenuItem className="text-destructive focus:text-destructive">
                            <Trash2 className="mr-2 h-4 w-4" /> Remove
                          </DropdownMenuItem>
                        </DropdownMenuContent>
                      </DropdownMenu>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Sidebar Info */}
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Workspace Usage</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <div className="flex items-center justify-between text-sm">
                  <span className="text-gray-400">Seats Used</span>
                  <span className="text-white font-medium">4 / 10</span>
                </div>
                <div className="h-2 w-full bg-white/10 rounded-full overflow-hidden">
                  <div className="h-full bg-emerald-500 w-[40%]" />
                </div>
              </div>
              <Button variant="outline" className="w-full">Manage Billing</Button>
            </CardContent>
          </Card>
          
          <Card className="bg-gradient-to-br from-blue-900/20 to-violet-900/20 border-blue-500/20">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-blue-400">
                <Shield className="h-5 w-5" />
                Security
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-gray-400 mb-4">
                Require SSO or Two-Factor Authentication for all workspace members.
              </p>
              <Button variant="secondary" className="w-full bg-blue-500/10 text-blue-400 hover:bg-blue-500/20 border border-blue-500/20">
                Configure Security
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
