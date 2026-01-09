// ExamTutor - No authentication required for now
// This middleware is intentionally empty to allow public access

import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export function middleware(request: NextRequest) {
  // Allow all requests through without authentication
  return NextResponse.next();
}

export const config = {
  matcher: [
    // Only match API routes if needed
    "/(api)(.*)",
  ],
};
