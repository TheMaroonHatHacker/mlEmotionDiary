"use client";

import { useState, FormEvent, ChangeEvent } from "react";
import { query } from "@/actions/query";

export function AiQuery() {
  return (
    <form action={query} className="form-control">
      <label className="label" htmlFor="Input">
        Input
      </label>
      <input
        className="input input-bordered mb-4"
        name="input"
        type="text"
        required
      />
    </form>
  );
}