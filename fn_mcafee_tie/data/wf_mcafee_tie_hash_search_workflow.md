<!--
    DO NOT MANUALLY EDIT THIS FILE
    THIS FILE IS AUTOMATICALLY GENERATED WITH resilient-circuits codegen
-->

# (Example) McAfee TIE hash search workflow

## Function - McAfee TIE search hash

### API Name
`mcafee_tie_search_hash`

### Output Name
``

### Message Destination
`mcafee_tie_md`

### Pre-Processing Script
```python
if artifact.type == "Malware MD5 Hash":
  inputs.mcafee_tie_hash_type = "md5"
  inputs.mcafee_tie_hash = artifact.value
elif artifact.type == "Malware SHA-1 Hash":
  inputs.mcafee_tie_hash_type = "sha1"
  inputs.mcafee_tie_hash = artifact.value
elif artifact.type == "Malware SHA-256 Hash":
  inputs.mcafee_tie_hash_type = "sha256"
  inputs.mcafee_tie_hash = artifact.value
else:
  helper.fail("Artifact hash was not set correctly")

```

### Post-Processing Script
```python
"""
Data returned will be in the following structure


{  
   "GTI":{  
      "File Provider":"GTI",
      "Attributes":{  

      },
      "Create Date":"2018-02-21 12:17:10",
      "Trust Level":"Known Malicious"
   },
   "ATD":{  
      "File Provider":"ATD",
      "Create Date":"2018-03-14 11:53:09",
      "Trust Level":"Most Likely Malicious"
   },
   "MWG":{  
      "File Provider":"MWG",
      "Create Date":"2018-03-14 11:53:55",
      "Trust Level":"Most Likely Malicious"
   },
   "Enterprise":{  
      "File Provider":"Enterprise",
      "Attributes":{  
         "Average Local Rep":"Most Likely Malicious",
         "First Contact":"2018-02-21 12:17:10",
         "Min Local Rep":"Most Likely Malicious",
         "Is Prevalent":"0",
         "File Name Count":"1",
         "Max Local Rep":"Most Likely Malicious"
      },
      "Create Date":"2018-02-21 12:17:10",
      "Trust Level":"Most Likely Malicious"
   }
   "system_list":[{
     "date": 1519233563,
     "agentGuid": {a00728ff-3187-46c1-97d2-8e0f26ea940b}
   }]
}
"""

row = incident.addRow("tie_results")
row["hash_type"] = artifact.type
row["hash"] = artifact.value
row["file_provider"] = results["Enterprise"]["File Provider"]
row["trust_level"] = results["Enterprise"]["Trust Level"]
row["tie_create_date"] = results["Enterprise"]["Create Date"]





```

---

