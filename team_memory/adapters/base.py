from copy import deepcopy
from team_memory.contracts.ports import VERSION
from team_memory.contracts.schema import OPERATIONS
from team_memory.contracts.validation import ContractError, validate, validate_exchange


class Failure(Exception):
    def __init__(self, code, message, *, retryable=False, item_id=None):
        self.issue = dict(code=code, message=message, retryable=retryable, item_id=item_id)
        super().__init__(message)


def issue(code, message, item_id=None):
    return dict(code=code,message=message,retryable=False,item_id=item_id)


def request(operation, payload, *, workspace_id, request_id):
    return dict(contract_version=VERSION,operation=operation,payload=payload,
                workspace_id=workspace_id,request_id=request_id)


class Adapter:
    module = ''
    capabilities = {}

    def __init__(self, workspace_id):
        self.workspace_id = workspace_id

    def verify_snapshot(self,snapshot):
        original=self.snapshot_loader(snapshot['id'])
        if original!=snapshot:raise Failure('EVIDENCE_INVALID','Snapshot differs from authoritative records')

    def handle(self, req, *, context):
        # Routing identifiers must be valid even in an invalid-input response.
        op = req.get('operation') if isinstance(req,dict) else None
        if op not in self.capabilities:
            raise ContractError('Request is not routable to this port')
        common = {k:req.get(k) for k in ('contract_version','request_id','workspace_id','operation')}
        common['module'] = self.module
        try:
            validate('request',req)
            if (context.workspace_id != self.workspace_id or req['workspace_id'] != self.workspace_id
                    or self.capabilities[op] not in context.capabilities):
                raise Failure('FORBIDDEN','Workspace or capability denied')
            data, errors = self.execute(op,deepcopy(req['payload']),context)
            response = dict(**common,status='partial' if errors else 'ok',data=data,errors=errors)
            validate_exchange(req,response)
            return response
        except Failure as exc:
            status = 'error' if exc.issue['code'] in ('IO_FAILURE','MODEL_TIMEOUT','RETRIEVAL_FAILED','MODEL_OUTPUT_INVALID') else 'invalid'
            return dict(**common,status=status,data=None,errors=[exc.issue])
        except (ContractError,ValueError,KeyError,TypeError) as exc:
            return dict(**common,status='invalid',data=None,errors=[issue('INVALID_INPUT',str(exc))])
        except OSError:
            return dict(**common,status='error',data=None,errors=[issue('IO_FAILURE','Storage operation failed')])

