<!--
    DO NOT MANUALLY EDIT THIS FILE
    THIS FILE IS AUTOMATICALLY GENERATED WITH resilient-circuits codegen
-->

# Example: Secureworks Close Ticket

## Function - Secureworks CTP Close Ticket

### API Name
`secureworks_ctp_close_ticket`

### Output Name
`None`

### Message Destination
`fn_secureworks_ctp`

### Pre-Processing Script
```python
inputs.incident_id = incident.id
```

### Post-Processing Script
```python
if results.success:
  noteText = u'Secureworks ticket {0} closed.'.format(results.content['ticketID'])
elif:
  noteText = u'ERROR: unable to close Secureworks CTP ticket {0}.'.format(results.content['ticketID']) 

incident.addNote(noteText)
```

---

