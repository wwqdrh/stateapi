SHELL := /bin/bash -o pipefail

.PHONY: dev
dev:
	MODE=dev python -m stateapi

.PHONY: dist
dist:
	rm -rf dist
	$(python) -m nuitka --module stateapi --include-package=stateapi --include-package=pykit --output-dir=dist
	poetry export --without-hashes -o dist/requirements.txt
	rm -rf dist/*.build

.PHONY py-tools:
py-tools:
	poetry add grpcio-tools protobuf "grpclib[protobuf]"

.PHONY proto-py:
proto-py:
	for i in `find $(CURDIR)/protos -type f -name "*.proto"`; do prefix="$(CURDIR)" python -m grpc_tools.protoc --proto_path=$(CURDIR) --pyi_out=$(CURDIR) --python_out=$(CURDIR) --grpc_python_out=$(CURDIR) $${i//$$prefix//} ; done

.PHONY go-tools:
go-tools:
#apt install -y protobuf-compiler
	go install google.golang.org/protobuf/cmd/protoc-gen-go@v1.28
	go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@v1.2

.PYONY proto-go:
proto-go:
	for i in `find $(CURDIR)/protos -type f -name "*.proto"`; do \
		prefix="$(CURDIR)" protoc --proto_path=$(CURDIR) \
		--go_out=. --go_opt=paths=source_relative \
		--go-grpc_out=require_unimplemented_servers=false:. --go-grpc_opt=paths=source_relative $${i//$$prefix//} ; \
	done

# 还是生成到与原路径一直是最好的，不需要修改路径问题
.PHONY proto-py-dist:
proto-py-dist:
	mkdir -p $(CURDIR)/dist

	temp_path=`mktemp -d` \
	&& cp -rf $(CURDIR)/protos $$temp_path \
	&& for i in `find $$temp_path/protos -type f -name "*.proto"`; do prefix="$$temp_path" python -m grpc_tools.protoc --proto_path=$$temp_path --python_out=$$temp_path --grpclib_python_out=$$temp_path $${i//$$prefix//} ; done \
	&& for i in `find $$temp_path/protos -type f -not -name "*.py"`; do rm $$i; done \
	&& cd $$temp_path && tar -zcvf $(CURDIR)/dist/proto-python-dist.tar.gz protos \
	&& rm -rf $$temp_path

.PHONY proto-go-dist:
proto-go-dist:
	mkdir -p $(CURDIR)/dist

	temp_path=`mktemp -d` \
	&& cp -rf $(CURDIR)/protos $$temp_path \
	&& for i in `find $(CURDIR)/protos -type f -name "*.proto"`; do \
		prefix="$(CURDIR)" protoc --proto_path=$(CURDIR) \
		--go_out=. --go_opt=paths=source_relative \
		--go-grpc_out=require_unimplemented_servers=false:. --go-grpc_opt=paths=source_relative $${i//$$prefix//} ; \
	done \
	&& for i in `find $$temp_path/protos -type f -not -name "*.go"`; do rm $$i; done \
	&& cd $$temp_path && tar -zcvf $(CURDIR)/dist/proto-go-dist.tar.gz protos \
	&& rm -rf $$temp_path