from fastapi import FastAPI,Depends,HTTPException
from sqlalchemy.orm import Session
from models.financas import Categoria
from models.financas import Transacoes
from conf.db_session import create_session
from schemas.schema import SchemaCategoria
from schemas.schema import SchemaTransacoes

app = FastAPI()


def get_db():

    db = create_session()
    try:
        yield db
    finally:
        db.close()

@app.get('/financa')

def root_teste(db: Session = Depends(get_db)):

    categoria = db.query(Categoria).all()
    transacoes = db.query(Transacoes).all()

    return transacoes,categoria


@app.post('/financa/gastos')

def post_gatos(cate: SchemaCategoria, tran: SchemaTransacoes, db: Session = Depends(get_db) ):

    nova_categoria: Categoria = Categoria(

        nome = cate.nome,
        descricao = cate.descricao

    )

    nova_transacao : Transacoes = Transacoes(
        tipo = tran.tipo,
        valor = tran.valor,
        descricao = tran.descricao,
        data = tran.data,
        categoria=nova_categoria

    )

    db.add(nova_categoria)
    db.commit()
    db.refresh(nova_categoria)
    db.add(nova_transacao)
    db.commit()
    db.refresh(nova_transacao)

    return {'Categoria/transações': f'{nova_categoria} -- {nova_transacao}'}

@app.put('/financa/atualizar/{id_categoria}/{id_transacao}')

def put_categoria_trasacoes(
    id_categoria:int ,
    id_transacao:int,
    nova_categaria: SchemaCategoria,
    nova_transacao: SchemaTransacoes,
    db: Session = Depends(get_db)):

    categoria = db.query(Categoria).filter(Categoria.id == id_categoria).first()
    transacoes = db.query(Transacoes).filter(Transacoes.id == id_transacao).first()



    if categoria:

        categoria.nome = nova_categaria.nome
        categoria.descricao = nova_categaria.descricao

        db.commit()
        db.refresh(categoria)


    if transacoes:

        transacoes.tipo = nova_transacao.tipo
        transacoes.valor = nova_transacao.valor
        transacoes.descricao = nova_transacao.descricao
        transacoes.data = nova_transacao.data

        db.commit()

        db.refresh(transacoes)


    return categoria,transacoes


@app.delete('/financa/delete/{id_categoria}')

def delete_categoria_transacoes(id_categoria: int, db: Session = Depends(get_db)):

    categoria = db.query(Categoria).filter(Categoria.id == id_categoria).first()
    transacoes = db.query(Transacoes).filter(Transacoes.id == id_categoria).first()

    if transacoes:
        db.delete(transacoes)
        db.commit()

    if categoria:
        db.delete(categoria)

        db.commit()  

    else:
        raise {'Mensagem': 'Catego não encontrada'}
    
    return {'Mensagem': f'Categoria {categoria.id} deletada com sucesso'}