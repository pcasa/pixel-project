# Personas

One directory per recipient. Each contains a `persona.json` seeded before shipping.

## Schema

```json
{
  "recipient_name": "Sarah",
  "recipient_role": "Product Manager at Acme Corp",
  "gift_from": "Peter",
  "onboarding_complete": false,
  "preferences": {},
  "memory": []
}
```

`onboarding_complete: false` triggers the first-launch interview on the hub.
After the interview completes, the hub writes preferences and memory back here.

## Adding a Recipient

```bash
tools/personalize.sh --name "Sarah Chen" --role "Product Manager at Acme" --dir sarah_chen
```

(Script TBD — Phase 5)
