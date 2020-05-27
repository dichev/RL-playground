import torch
from logging import warning

device = 'cpu'
built_with_cuda = torch.cuda.is_available()
if built_with_cuda:
    try:
        print(torch.cuda.FloatTensor([1]))  # test is cuda really working
        device = 'cuda'
    except Exception as err:
        warning(str(err))

print(f'[info] PyTorch: using {device.upper()} device')
if device == 'cuda':
    torch.device('cuda')
    torch.set_default_tensor_type(torch.cuda.FloatTensor)

__all__ = []