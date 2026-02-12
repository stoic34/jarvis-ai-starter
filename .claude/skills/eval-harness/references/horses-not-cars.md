# Horses, Not Cars

## The Mental Model

When people first use AI assistants, they expect **car behavior**:
- Turn the steering wheel left → the car goes left
- Press the brake → the car stops
- Every input produces a predictable, deterministic output

But AI assistants are more like **horses**:
- Kick to go → the horse *usually* goes
- Pull the reins left → the horse *mostly* turns left
- The horse has its own tendencies, strengths, and blind spots
- Sometimes it takes the scenic route
- Sometimes it stops to eat grass

## Why This Matters

If you expect a car and get a horse, you'll be frustrated when it doesn't follow instructions perfectly. You might conclude the technology doesn't work.

But if you expect a horse, you'll:
1. **Give clear directions** — not ambiguous ones
2. **Check that it's going the right way** — not assume
3. **Correct course early** — not wait until you're lost
4. **Reward good behavior** — reinforce what works

## Eval Harnesses = Reins and Spurs

An eval harness is the set of tools that keep the horse on track:

- **Checklist** = the map (where are we going?)
- **Step verification** = checking the compass (are we on track?)
- **Pass/fail criteria** = the fence (don't go past this boundary)
- **Final report** = the destination check (did we arrive?)

Without an eval harness, the horse might:
- Claim it arrived when it's still on the road (lazy completion)
- Take a different route than you wanted (scope drift)
- Stop partway and call it done (partial completion)

With an eval harness, these failure modes are caught immediately.

## Practical Application

**Without eval harness:**
> "Set up the project"
> *Agent does 5 things, reports "Done!"*
> *You check and find 2 of 5 things are wrong*

**With eval harness:**
> "Set up the project with an eval harness"
> *Agent creates checklist of 5 steps*
> *Executes and verifies each step*
> *Reports: "4/5 PASS, step 3 FAIL — here's what happened"*
> *You know exactly what needs fixing*

The second approach takes slightly longer but is dramatically more reliable.

## When to Ride Without Reins

Simple tasks don't need eval harnesses:
- "What's on my calendar today?" — just check and report
- "Add this to my inbox" — one step, easily verified
- Quick lookups, simple questions, casual conversation

The eval harness is for **multi-step work where getting it wrong matters**.
